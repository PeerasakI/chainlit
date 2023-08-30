import chainlit as cl
import openai
import os
from chainlit.prompt import Prompt, PromptMessage
from chainlit.playground.providers import ChatOpenAI
from psw.key import Keys



cls_key = Keys()
openai.api_key = cls_key.openai_key

# _input = 'Compute the number of customers who watched more than 50 minutes of video this month'
# template = """SQL tables (and columns):
# * Customers(customer_id, signup_date)
# * Streaming(customer_id, video_id, watch_date, watch_minutes)

# A well-written SQL query that {input}:
# ```"""
template = """SQL tables (and columns):
* pointx_fbs_txn_rpt_dly (event_name, customer_id, user_pseudo_id,
user_id, event_previous_timestamp, event_value_in_usd,
event_server_timestamp_offset, privacy_info_analytics_storage,
privacy_info_ads_storage, privacy_info_uses_transient_token,
user_properties_ga_session_number, user_properties_ga_session_number_set_timestamp_micros,
user_properties_ga_session_id, user_properties_ga_session_id_set_timestamp_micros,
user_properties_first_open_time, user_properties_first_open_time_set_timestamp_micros,
user_first_touch_timestamp, user_ltv_revenue, user_ltv_currency, device_category,
device_mobile_brand_name, device_mobile_model_name, device_mobile_marketing_name,
device_mobile_os_hardware_model, device_operating_system, device_operating_system_version,
device_vendor_id, device_advertising_id, device_language, device_is_limited_ad_tracking,
device_time_zone_offset_seconds, device_browser, device_browser_version,
device_web_info_browser, device_web_info_browser_version, device_web_info_hostname,
geo_continent, geo_country, geo_region, geo_city, geo_sub_continent, geo_metro,
app_info_id, app_info_version, app_info_install_store, app_info_firebase_app_id,
app_info_install_source, traffic_source_name, traffic_source_medium, traffic_source_source,
stream_id, platform, event_dimensions_hostname, ecommerce, items, source_date, address_id,
auto_earn_display, banner_description, banner_rank, banner_title, campaign,
campaign_info_source, card_sub_product, change_language, coupon_id, customer_device_lat,
customer_device_long, customer_lat, customer_long, customer_type, deal_title, deal_type,
debug_event, deleteacount_button, delivery_address, delivery_fee, delivery_option,
delivery_type, e_coupon_display, each_point_card, ecatalog_list, ecatalog_rank,
ecoupon_rank, ecoupon_title, engaged_session_event, engagement_time_msec, entrances,
error_message, error_value, event_id, fatal, firebase_conversion, firebase_error,
firebase_event_origin, firebase_previous_class, firebase_previous_id, firebase_previous_screen,
firebase_screen, firebase_screen_class, firebase_screen_id, flashdeals_rank,
flashdeals_title, from_customer_name, from_customer_profile_name, ga_session_id,
ga_session_number, id, ignore_referrer, item_code, latitude, longitude, link_classes,
link_domain, link_url, list_card_sub_product, list_each_point_card, medium, merchant_id,
message_type, offer_type, order_id, order_status, outbound, page, page_location, 
page_referrer, page_title, payment_method, percent_scrolled, place_id, place_lat, 
place_long, place_name, point_balance_display, points, points_per_unit, points_remaining, 
previous_app_version, previous_first_open_count, previous_os_version, primary_address, 
product_id, quantity, reason_id, recommendedForYou_rank, search_list_id, 
search_list_id_scan_and_pay, search_list_id_xstore, session_engaged, shop_list_id, 
sku_catagory_name, sku_group_type, sku_id, source, source_page_name, stock_code, 
system_app, system_app_update, tab_name, term, text_search, timestamp, to_customer_name, 
to_customer_profile_name, toggle, total_amount, total_point, total_points, transaction_id, 
transaction_status, transaction_type, unable_to_proceed, update_with_analytics, client_code, 
client_member_id, _dl_load_ts, _date)
A well-written SQL query that {input}:
```"""
settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"],
}

# @cl.on_message
# async def main(msg:str):
#     resp = msg.title()
#     await cl.Message(content = f"here is a message{resp}").send()

@cl.on_message
async def main(message: str):
    # Create the prompt object for the Prompt Playground
    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="user",
                template=template,
                formatted=template.format(input=message)
            )
        ],
        settings=settings,
        inputs={"input": message},
    )

    # Prepare the message for streaming
    msg = cl.Message(
        content="",
        language="sql",
    )

    # Call OpenAI
    async for stream_resp in await openai.ChatCompletion.acreate(
        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
    ):
        token = stream_resp.choices[0]["delta"].get("content", "")
        await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    # Send and close the message stream
    await msg.send()


    