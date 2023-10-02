"""
    The Charges (Units) per page are like below:
    Scanned : 1
    Not Scanned : 0.5
    Images : 1

    Initially assessment will be done based on Scanned, once the feedback
    from other microservice discovers that the pdf uploaded in not scanned
    the 50% credits will be refunded
"""

SCANNED_CHARGE = 1.0
NOT_SCANNED_CHARGE = 0.5


class Credit_Logic:
    @staticmethod
    def debit(num_pages_scanned: int, num_pages_not_scanned: int, current_credits: float) -> float:
        return current_credits - (SCANNED_CHARGE * num_pages_scanned) - (NOT_SCANNED_CHARGE * num_pages_not_scanned)

    @staticmethod
    def refund_corrected(actual_scanned: int,
                         actual_not_scanned: int,
                         predicted_scanned: int,
                         predicted_not_scanned: int,
                         current_credits: float):
        return current_credits + (actual_scanned * SCANNED_CHARGE) + (actual_not_scanned * NOT_SCANNED_CHARGE) - \
            (predicted_scanned * SCANNED_CHARGE) - (predicted_not_scanned * NOT_SCANNED_CHARGE)
