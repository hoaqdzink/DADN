import io
import json
from config.config import Config
from db.repository import users, data_files, mongo_data_file, features
from pkg import date_time, hash, crypt, file_process, s3
from pkg.logger import logger
from pkg.features_module import calculate_feature
from config.message import Message as msg
from typing import Tuple, Dict, List, Optional

KEY: Dict[str, dict] = {
    "sample_name": {"type": str, "max_length": 255},
    "number_of_measurements": {"type": int},
    "measurement_number": {"type": int},
    "board_name": {"type": str, "max_length": 255},
    "measurement_method": {"type": str, "max_length": 255},
    "tag": {"type": (list, dict)},
    "project_name": {"type": str, "max_length": 255},
    "device_name": {"type": str, "max_length": 255},
    "measurement_date": {"type": str},
    "AD_frequency[Hz]": {"type": int},
    "AD_gain": {"type": int},
    "number_of_sequences": {"type": int},
    "AD_time_start": {"type": str},
    "memo": {"type": str, "max_length": 255},
    "repeat_interval[sec.]": {"type": (float, int)},
}

# Declare Threshold
MIN_VALUE = -9999
MAX_VALUE = 9999


def validate_file(user_id: int, data: str) -> Tuple[bool, dict, dict]:
    try:
        json_data = json.loads(data)
    except Exception as e:
        logger.error(e)
        return False, {}, {"message": msg.file["invalid_json"]}
    # Check Data type and Key
    ad_information = json_data["AD"]["information"]
    key_list = ad_information.keys()
    for key, value in KEY.items():
        if key not in key_list:
            return (
                False,
                {},
                {"message": msg.file["not_found_key"].format(key=key)},
            )
        if not isinstance(ad_information[key], value["type"]):
            return (
                False,
                {},
                {
                    "message": msg.file["wrong_datatype"].format(
                        key=key, type=str(value["type"])
                    )
                },
            )
        if "max_length" in data:
            if len(ad_information[key]) > value["max_length"]:
                return (
                    False,
                    {},
                    {
                        "message": msg.file["exceed_max_length"].format(
                            key=key,
                            len=len(ad_information[key]),
                            max_len=value["max_length"],
                        )
                    },
                )

    try:
        json_data["AD"]["information"][
            "measurement_date"
        ] = date_time.convert_str_to_datetime(ad_information["measurement_date"])
    except Exception as e:
        logger.error(e)
        return (
            False,
            {},
            {"message": msg.file["wrong_value"].format(value="measurement_date")},
        )

    try:
        json_data["AD"]["information"][
            "AD_time_start"
        ] = date_time.convert_str_to_datetime(
            ad_information["AD_time_start"], "%y/%m/%d %H:%M:%S"
        )
    except Exception as e:
        logger.error(e)
        return (
            False,
            {},
            {"message": msg.file["wrong_value"].format(value="AD_time_start")},
        )

    # Check Sensor have valid data for all channels and Threshold
    volt_data_list = {
        key: value for key, value in json_data["AD"]["AD_data"].items() if "ch" in key
    }
    for key in volt_data_list:
        if len(volt_data_list[key]) == 0:
            return (
                False,
                {},
                {"message": msg.file["key_value_null"].format(key=key)},
            )
        for value in volt_data_list[key]:
            if not isinstance(value, float):
                return (
                    False,
                    {},
                    {
                        "message": msg.file["key_type_error"].format(
                            key=key, type="float"
                        )
                    },
                )
            if value > MAX_VALUE or value < MIN_VALUE:
                return (
                    False,
                    {},
                    {
                        "message": msg.file["threshold_invalid"].format(
                            key=key, min=MIN_VALUE, max=MAX_VALUE
                        )
                    },
                )

    # Check file is uploaded or not
    data_hash = hash.hash_file(data)
    hash_files = data_files.get_hash_by_user_id(user_id)
    for hash_file in hash_files:
        if data_hash == hash_file.hash:
            return False, {}, {"message": msg.file["exist"]}
    json_data["hash"] = data_hash
    return True, json_data, {}


def save_features(data_files_id: int, values: dict):
    features_list = []
    for channel in values:
        for feature_id in values[channel]:
            features_list.append(
                {
                    "data_file_id": data_files_id,
                    "feature_id": feature_id,
                    "channel": channel,
                    "value": values[channel][feature_id],
                }
            )

    features.add_features(features_list)


def convert_body(
    id: int, file_name: str, time_data: list, volt_data: dict, ad_information: dict
) -> dict:
    tags = ad_information["tag"]
    return {
        "id": id,
        "file_name": file_name,
        "sample_name": f'{ad_information["sample_name"]}_{ad_information["measurement_number"]}_{date_time.convert_datetime_to_string(ad_information["measurement_date"], "%Y%m%d_%H%M%S")}',
        "project_name": ad_information["project_name"],
        "measurements": ad_information["measurement_number"],
        "board_name": ad_information["board_name"],
        "measurement_method": ad_information["measurement_method"],
        "device_name": ad_information["device_name"],
        "measurement_date": str(ad_information["measurement_date"]),
        "ad_freq_hz": ad_information["AD_frequency[Hz]"],
        "ad_gain": ad_information["AD_gain"],
        "sequences": ad_information["number_of_sequences"],
        "ad_start_time": str(ad_information["AD_time_start"]),
        "repeat_interval_seconds": ad_information["repeat_interval[sec.]"],
        "tag1": "" if len(tags) < 1 else tags[0],
        "tag2": "" if len(tags) < 2 else tags[1],
        "tag3": "" if len(tags) < 3 else tags[2],
        "memo": ad_information["memo"],
        "data": {"time_data": time_data, "data": volt_data, "title": file_name},
    }


def upload_file(email: str, file_name: str) -> Tuple[int, dict]:
    user_id = users.get_id_by_email(email)
    data = b""
    # check file name
    prefixes = s3.list_prefixes(Config.S3_BUCKET, f"tmp/{user_id}/")
    files_name = [prefix.split("/")[-1] for prefix in prefixes]
    if file_name not in files_name:
        return 400, {"message": msg.file["not_exist"]}
    else:
        tmp_prefix = f"tmp/{user_id}/{file_name}"
        data = s3.get_object(Config.S3_BUCKET, tmp_prefix)
        s3.delete_object(Config.S3_BUCKET, tmp_prefix)

    # Decrypt file
    try:
        bytes_data = crypt.aes_128_ecb_decryption(data)
        str_data = bytes_data.decode("utf-8-sig")
    except Exception as e:
        logger.error(e)
        return 400, {"message": msg.file["invalid"]}

    # Validate File
    is_validate, data_json, message = validate_file(user_id, str_data)
    if not is_validate:
        return 400, message

    # Save information to data_files table
    ad_information = data_json["AD"]["information"]
    data_files_id = data_files.add_data_file(
        user_id,
        file_name,
        ad_information["sample_name"],
        ad_information["number_of_measurements"],
        ad_information["measurement_number"],
        ad_information["board_name"],
        ad_information["measurement_method"],
        ad_information["tag"],
        ad_information["project_name"],
        ad_information["device_name"],
        ad_information["measurement_date"],
        ad_information["AD_frequency[Hz]"],
        ad_information["AD_gain"],
        ad_information["number_of_sequences"],
        ad_information["AD_time_start"],
        ad_information["memo"],
        ad_information["repeat_interval[sec.]"],
        data_json["hash"],
        False,
    )

    # Upload file to S3
    is_success = s3.upload_object(
        Config.S3_BUCKET,
        f"sanyokasei/tmp/{data_files_id}.json",
        io.BytesIO(str_data.encode(encoding="utf-8")),
    )
    if not is_success:
        data_files.delete_data_files_by_id(data_files_id)
        return 500, {"message": msg.file["s3_upload_fail"]}

    volt_data = {
        key: value for key, value in data_json["AD"]["AD_data"].items() if "ch" in key
    }
    time_data = data_json["AD"]["AD_data"]["AD_Time[msec]"]
    volt_data, time_data = file_process.change_msec_to_sec(volt_data, time_data)
    return 200, convert_body(
        data_files_id, file_name, time_data, volt_data, ad_information
    )


def confirm_upload_file(
    email: str, data_files_id: int, tags: str, memo: str
) -> Tuple[int, dict]:
    try:
        tags = json.loads(tags)
    except Exception as e:
        logger.error(e)
        return 400, {"message": msg.file["tag_invalid"]}
    user_id = users.get_id_by_email(email)

    data_files_ids = data_files.get_data_files_id()
    if data_files_id not in data_files_ids:
        return 404, {"message": msg.file["not_found"].format(id=data_files_id)}

    data_files_ids = data_files.get_data_files_id_not_confirmed_by_user_id(user_id)
    if data_files_id not in data_files_ids:
        return 400, {"message": msg.file["unauthorized"]}

    # Check file is confirmed or not
    is_updated = data_files.get_is_upload_complete_by_id(data_files_id)
    if is_updated:
        return 200, {"message": msg.file["already_confirm"].format(id=data_files_id)}

    data = s3.get_object(
        Config.S3_BUCKET, f"sanyokasei/tmp/{data_files_id}.json"
    ).decode(encoding="utf-8")
    json_data = json.loads(data)

    # Get features of data
    try:
        features_calculation = calculate_feature.calculate_feature(json_data)
    except Exception as e:
        logger.error(e)
        return 400, {"message": msg.file["cal_feature_fail"]}

    # Copy file to sanyokasei/data/{data_files_id}.json
    is_success = s3.move_object(
        Config.S3_BUCKET,
        f"sanyokasei/tmp/{data_files_id}.json",
        f"sanyokasei/data/{data_files_id}.json",
    )
    if not is_success:
        return 500, {"message": "Server error"}

    # Save features of data to features table
    save_features(data_files_id, features_calculation)

    # Down Sample Data from 100Hz to 20Hz and save it to mongoDB
    down_sample_data = file_process.down_sample(json_data)
    down_sample_data["AD"]["information"]["repeat_interval[sec]"] = down_sample_data[
        "AD"
    ]["information"]["repeat_interval[sec.]"]
    del down_sample_data["AD"]["information"]["repeat_interval[sec.]"]
    is_success, key_id = mongo_data_file.add_data_file(data_files_id, down_sample_data)
    if not is_success:
        s3.move_object(
            Config.S3_BUCKET,
            f"sanyokasei/data/{data_files_id}.json",
            f"sanyokasei/tmp/{data_files_id}.json",
        )
        return 500, {"message": "Server error"}

    # Update column is_upload_complete of table data_files
    is_success = data_files.update_is_upload_complete_by_id(
        data_files_id, True, memo, tags
    )
    if not is_success:
        s3.move_object(
            Config.S3_BUCKET,
            f"sanyokasei/data/{data_files_id}.json",
            f"sanyokasei/tmp/{data_files_id}.json",
        )
        mongo_data_file.delete_data_file_by_id(data_files_id)
        return 500, {"message": "Server error"}

    return 200, {"message": msg.success}


def delete_files(email, data_files_ids: List[int]) -> Tuple[int, dict]:
    # Confirm ids:
    user_id = users.get_id_by_email(email)
    user_data_files_ids = data_files.get_data_files_id_by_user_id(user_id)
    logger.info(f"Delete data files {data_files_ids} by user {email}")

    all_data_files_ids = data_files.get_data_files_id()
    for data_files_id in data_files_ids:
        if data_files_id not in all_data_files_ids:
            logger.info(f"{data_files_id} not found")
            return 404, {"message": msg.file["not_found"].format(id=data_files_id)}

    for data_files_id in data_files_ids:
        if data_files_id not in user_data_files_ids:
            logger.info(
                f"user id {user_id} doesn't have permission to delete data_files {data_files_id}"
            )
            return 400, {"message": msg.file["unauthorized"]}

    for data_files_id in data_files_ids:
        # TODO It should be the transaction
        # Delete file in S3
        is_success = s3.delete_object(
            Config.S3_BUCKET, f"sanyokasei/tmp/{data_files_id}.json"
        )
        if not is_success:
            logger.error(f"Can not delete data file id {data_files_id} in S3")
            return 500, {"message": msg.fail}

        # Delete data file in mongoDB
        is_success = mongo_data_file.delete_data_file_by_id(data_files_id)
        if not is_success:
            logger.error(f"Can not delete data file id {data_files_id} in mongoDB")
            return 500, {"message": msg.fail}

        # Delete data_files
        is_success = data_files.delete_data_files_by_id(data_files_id)
        if not is_success:
            logger.error(f"Can not delete data file id {data_files_id} in DB")
            return 500, {"message": msg.fail}
    return 200, {"message": msg.success}


def get_list_files_not_confirmed(email) -> List[int]:
    user_id = users.get_id_by_email(email)
    data_files_ids = data_files.get_data_files_id_not_confirmed_by_user_id(user_id)
    return data_files_ids


def get_file(data_files_id: Optional[int], email: str) -> Tuple[bool, dict]:
    user_id = users.get_id_by_email(email)
    data_file = data_files.get_data_file_not_confirmed_by_user_id(
        user_id, data_files_id
    )
    if not data_file:
        return False, {"message": msg.file["not_exist"]}
    data = s3.get_object(
        Config.S3_BUCKET, f"sanyokasei/tmp/{data_file.id}.json"
    ).decode(encoding="utf-8")
    # data = open(r'D:\\SANYO\\file\\651.json', encoding='utf-8').read()
    if data == "":
        return False, {"message": msg.file["s3_get_fail"]}
    json_data = json.loads(data)
    volt_data = {
        key: value for key, value in json_data["AD"]["AD_data"].items() if "ch" in key
    }
    time_data = json_data["AD"]["AD_data"]["AD_Time[msec]"]
    volt_data, time_data = file_process.change_msec_to_sec(volt_data, time_data)
    ad_information = json_data["AD"]["information"]
    ad_information["measurement_date"] = date_time.convert_str_to_datetime(
        ad_information["measurement_date"]
    )
    return True, convert_body(
        data_file.id, data_file.file_name, time_data, volt_data, ad_information
    )


def delete_files_not_confirmed(email) -> bool:
    data_files_ids = get_list_files_not_confirmed(email)
    status_code, message = delete_files(email, data_files_ids)
    if status_code == 200:
        return True
    return False


def get_upload_presigned_url(email, file_name) -> str:
    user_id = users.get_id_by_email(email)
    presigned_url = s3.get_post_presigned_url(
        Config.S3_BUCKET, f"tmp/{user_id}/{file_name}", 7200
    )
    return presigned_url
