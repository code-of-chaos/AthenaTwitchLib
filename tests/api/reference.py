# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest
import os

# Athena Packages
from AthenaTwitchLib.api.api_connection import ApiConnection
import AthenaTwitchLib.api.api_requests as ApiRequests

from AthenaLib.parsers.dot_env import AthenaDotEnv

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestApiReference(unittest.IsolatedAsyncioTestCase):

    @staticmethod
    def _connection() -> ApiConnection:
        AthenaDotEnv(filepath=".secrets/secrets.env", auto_run=True)

        return ApiConnection(
            username=os.getenv("TWITCH_BROADCASTER_NAME"),
            oath_token=os.getenv("TWITCH_BROADCASTER_OATH"),
            client_id=os.getenv("TWITCH_BROADCASTER_CLIENT_ID")
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Tests -
    # ------------------------------------------------------------------------------------------------------------------
    async def test_start_commercial(self):
        async with self._connection() as api_connection:
            async for item in api_connection.request(ApiRequests.start_commercial(length=30)):
                print(item)

    async def test_get_extension_analytics(self):
        raise NotImplementedError

    async def test_get_game_analytics(self):
        raise NotImplementedError

    async def test_get_bits_leaderboard(self):
        raise NotImplementedError

    async def test_get_cheermotes(self):
        raise NotImplementedError

    async def test_get_extension_transactions(self):
        raise NotImplementedError

    async def test_get_channel_information(self):
        raise NotImplementedError

    async def test_modify_channel_information(self):
        raise NotImplementedError

    async def test_get_channel_editors(self):
        raise NotImplementedError

    async def test_create_custom_rewards(self):
        raise NotImplementedError

    async def test_delete_custom_reward(self):
        raise NotImplementedError

    async def test_get_custom_reward(self):
        raise NotImplementedError

    async def test_get_custom_reward_redemption(self):
        raise NotImplementedError

    async def test_update_custom_reward(self):
        raise NotImplementedError

    async def test_update_redemption_status(self):
        raise NotImplementedError

    async def test_get_charity_campaign(self):
        raise NotImplementedError

    async def test_get_charity_campaign_donations(self):
        raise NotImplementedError

    async def test_get_chatters(self):
        raise NotImplementedError

    async def test_get_channel_emotes(self):
        async with self._connection() as api_connection:
            async for item in api_connection.request(ApiRequests.get_channel_emotes()):
                print(item)

    async def test_get_global_emotes(self):
        async with self._connection() as api_connection:
            async for item in api_connection.request(ApiRequests.get_global_emotes()):
                print(item)

    async def test_get_emote_sets(self):
        raise NotImplementedError

    async def test_get_channel_chat_badges(self):
        raise NotImplementedError

    async def test_get_global_chat_badges(self):
        raise NotImplementedError

    async def test_get_chat_settings(self):
        raise NotImplementedError

    async def test_update_chat_settings(self):
        raise NotImplementedError

    async def test_send_chat_announcement(self):
        raise NotImplementedError

    async def test_get_user_chat_color(self):
        raise NotImplementedError

    async def test_update_user_chat_color(self):
        raise NotImplementedError

    async def test_create_clip(self):
        raise NotImplementedError

    async def test_get_clips(self):
        raise NotImplementedError

    async def test_get_code_status(self):
        raise NotImplementedError

    async def test_get_drops_entitlements(self):
        raise NotImplementedError

    async def test_update_drops_entitlements(self):
        raise NotImplementedError

    async def test_redeem_code(self):
        raise NotImplementedError

    async def test_get_extension_configuration_segment(self):
        raise NotImplementedError

    async def test_set_extension_configuration_segment(self):
        raise NotImplementedError

    async def test_set_extension_required_configuration(self):
        raise NotImplementedError

    async def test_send_extension_pubsub_message(self):
        raise NotImplementedError

    async def test_get_extension_live_channels(self):
        raise NotImplementedError

    async def test_get_extension_secrets(self):
        raise NotImplementedError

    async def test_create_extension_secret(self):
        raise NotImplementedError

    async def test_send_extension_chat_message(self):
        raise NotImplementedError

    async def test_get_extensions(self):
        raise NotImplementedError

    async def test_get_released_extensions(self):
        raise NotImplementedError

    async def test_get_extension_bits_products(self):
        raise NotImplementedError

    async def test_update_extension_bits_product(self):
        raise NotImplementedError

    async def test_create_eventsub_subscription(self):
        raise NotImplementedError

    async def test_delete_eventsub_subscription(self):
        raise NotImplementedError

    async def test_get_eventsub_subscriptions(self):
        raise NotImplementedError

    async def test_get_top_games(self):
        raise NotImplementedError

    async def test_get_games(self):
        raise NotImplementedError

    async def test_get_creator_goals(self):
        raise NotImplementedError

    async def test_get_hype_train_events(self):
        raise NotImplementedError

    async def test_check_automod_status(self):
        raise NotImplementedError

    async def test_manage_held_automod_messages(self):
        raise NotImplementedError

    async def test_get_automod_settings(self):
        raise NotImplementedError

    async def test_update_automod_settings(self):
        raise NotImplementedError

    async def test_get_banned_users(self):
        raise NotImplementedError

    async def test_ban_user(self):
        raise NotImplementedError

    async def test_unban_user(self):
        raise NotImplementedError

    async def test_get_blocked_terms(self):
        raise NotImplementedError

    async def test_add_blocked_term(self):
        raise NotImplementedError

    async def test_remove_blocked_term(self):
        raise NotImplementedError

    async def test_delete_chat_messages(self):
        raise NotImplementedError

    async def test_get_moderators(self):
        raise NotImplementedError

    async def test_add_channel_moderator(self):
        raise NotImplementedError

    async def test_remove_channel_moderator(self):
        raise NotImplementedError

    async def test_get_vips(self):
        raise NotImplementedError

    async def test_add_channel_vip(self):
        raise NotImplementedError

    async def test_remove_channel_vip(self):
        raise NotImplementedError

    async def test_get_polls(self):
        raise NotImplementedError

    async def test_create_poll(self):
        raise NotImplementedError

    async def test_end_poll(self):
        raise NotImplementedError

    async def test_get_predictions(self):
        raise NotImplementedError

    async def test_create_prediction(self):
        raise NotImplementedError

    async def test_end_prediction(self):
        raise NotImplementedError

    async def test_start_a_raid(self):
        raise NotImplementedError

    async def test_cancel_a_raid(self):
        raise NotImplementedError

    async def test_get_channel_stream_schedule(self):
        raise NotImplementedError

    async def test_get_channel_icalendar(self):
        raise NotImplementedError

    async def test_update_channel_stream_schedule(self):
        raise NotImplementedError

    async def test_create_channel_stream_schedule_segment(self):
        raise NotImplementedError

    async def test_update_channel_stream_schedule_segment(self):
        raise NotImplementedError

    async def test_delete_channel_stream_schedule_segment(self):
        raise NotImplementedError

    async def test_search_categories(self):
        raise NotImplementedError

    async def test_search_channels(self):
        raise NotImplementedError

    async def test_get_soundtrack_current_track(self):
        raise NotImplementedError

    async def test_get_soundtrack_playlist(self):
        raise NotImplementedError

    async def test_get_soundtrack_playlists(self):
        raise NotImplementedError

    async def test_get_stream_key(self):
        raise NotImplementedError

    async def test_get_streams(self):
        raise NotImplementedError

    async def test_get_followed_streams(self):
        raise NotImplementedError

    async def test_create_stream_marker(self):
        raise NotImplementedError

    async def test_get_stream_markers(self):
        raise NotImplementedError

    async def test_get_broadcaster_subscriptions(self):
        raise NotImplementedError

    async def test_check_user_subscription(self):
        raise NotImplementedError

    async def test_get_all_stream_tags(self):
        raise NotImplementedError

    async def test_get_stream_tags(self):
        raise NotImplementedError

    async def test_replace_stream_tags(self):
        raise NotImplementedError

    async def test_get_channel_teams(self):
        raise NotImplementedError

    async def test_get_teams(self):
        raise NotImplementedError

    async def test_get_users(self):
        raise NotImplementedError

    async def test_update_user(self):
        raise NotImplementedError

    async def test_get_users_follows(self):
        raise NotImplementedError

    async def test_get_user_block_list(self):
        raise NotImplementedError

    async def test_block_user(self):
        raise NotImplementedError

    async def test_unblock_user(self):
        raise NotImplementedError

    async def test_get_user_extensions(self):
        raise NotImplementedError

    async def test_get_user_active_extensions(self):
        raise NotImplementedError

    async def test_update_user_extensions(self):
        raise NotImplementedError

    async def test_get_videos(self):
        raise NotImplementedError

    async def test_delete_videos(self):
        raise NotImplementedError

    async def test_send_whisper(self):
        raise NotImplementedError