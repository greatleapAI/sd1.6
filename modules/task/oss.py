# coding=utf-8
from PIL import Image
import oss2
from io import BytesIO
from snowflake import SnowflakeGenerator
import requests
import json

auth = oss2.Auth("LTAI5tQnLUQgZSY9xy7rz2fL", "eIVPKw6R7eSv2Mt2EJ6ZJJ9Rh3HKqJ")
bucket = oss2.Bucket(
    auth, 'oss-cn-hangzhou.aliyuncs.com/', 'zy-pic-items-test')


aigc_id_gen = SnowflakeGenerator(1023)
REMEMBER_COOKIE_NAME = 'greatleapai_token'


def gen_aigc_oss_id():
    val = next(aigc_id_gen)
    return val


def upload_to_oss(images_gen) -> bool:

    images = []

    for image in images_gen:
        id = gen_aigc_oss_id()
        oss_name = "{}.png".format(id)

        buf = BytesIO()
        image.save(buf, 'png')

        img_data = buf.getvalue()
        result = bucket.put_object(oss_name, img_data)
        buf.close()

        images.append({
            "url": "https://cdn.greatleapai.com/{}".format(oss_name),
            "bucket": "zy-pic-items-test",
            "size": len(img_data)
        })

    return True, images