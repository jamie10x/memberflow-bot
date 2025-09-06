# backend/app/services/ton_service.py
import logging
from pytonapi import Tonapi
from pytonapi.exceptions import TONAPIError

class TONService:
    def __init__(self, api_key: str):
        self.tonapi = Tonapi(api_key=api_key)

    async def find_and_verify_transaction(
            self,
            recipient_address: str,
            expected_amount: int, # in nano-units (e.g., nanotons or nano-USDT)
            expected_memo: str
    ) -> bool:
        """
        Scans the recent transactions of a wallet to find and verify a specific payment.

        :param recipient_address: The wallet address that should have received the funds.
        :param expected_amount: The exact amount (in nano-units) that should have been sent.
        :param expected_memo: The unique comment/memo that identifies this transaction.
        :return: True if a valid transaction is found, False otherwise.
        """
        try:
            logging.info(f"Searching for transaction to {recipient_address} with memo {expected_memo}")

            # Get the last 100 transactions for the recipient's account
            # In a high-volume system, you might need more sophisticated paging/searching.
            account_events = await self.tonapi.accounts.get_events(account_id=recipient_address, limit=100)

            for event in account_events.events:
                for action in event.actions:
                    # We are looking for an incoming TonTransfer or JettonTransfer
                    if action.simple_preview.name in ("Ton Transfer", "Jetton Transfer"):
                        if action.ton_transfer and action.ton_transfer.comment == expected_memo:
                            received_amount = action.ton_transfer.amount
                            logging.info(f"Found matching TON transfer with amount: {received_amount}")
                            if received_amount >= expected_amount:
                                logging.info("VERIFICATION SUCCESS: Amount is sufficient.")
                                return True

                        elif action.jetton_transfer and action.jetton_transfer.comment == expected_memo:
                            received_amount = action.jetton_transfer.amount
                            logging.info(f"Found matching Jetton (USDT) transfer with amount: {received_amount}")
                            # Note: Jetton amounts are strings, they need to be converted to int
                            if int(received_amount) >= expected_amount:
                                logging.info("VERIFICATION SUCCESS: Amount is sufficient.")
                                return True

            logging.warning(f"Verification FAILED: No matching transaction found for memo {expected_memo}")
            return False

        except TONAPIError as e:
            logging.error(f"TON API Error during verification: {e}")
            return False
        except Exception as e:
            logging.exception(f"Unexpected error during TON verification: {e}")
            return False