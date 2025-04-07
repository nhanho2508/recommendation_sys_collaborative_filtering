import os
import sys
import traceback


class AppException(Exception):
    """
    Custom exception class to enrich error details with traceback context.
    Useful for debugging by showing filename, line number, and the actual error message.
    """

    def __init__(self, error_message: Exception, error_detail: sys):
        """
        Initialize AppException with detailed error trace.

        Input:
        - error_message: Exception object that was raised
        - error_detail: sys module to access traceback info

        Output:
        - Sets self.error_message with detailed info
        """
        super().__init__(error_message)
        self.error_message = self._format_error_message(error_message, error_detail)

    @staticmethod
    def _format_error_message(error: Exception, error_detail: sys) -> str:
        """
        Build detailed error message with file name and line number.

        Input:
        - error: the exception instance
        - error_detail: sys module to fetch traceback

        Output:
        - A formatted string message containing traceback info
        """
        _, _, traceback_obj = error_detail.exc_info()
        if traceback_obj is not None:
            file_path = traceback_obj.tb_frame.f_code.co_filename
            line_number = traceback_obj.tb_lineno
            message = (
                f"\n[AppException]: An error occurred in file: '{file_path}'\n"
                f"   → Line Number: {line_number}\n"
                f"   → Error: {str(error)}"
            )
        else:
            message = f"\n[AppException]: {str(error)} (No traceback available)"
        return message

    def __str__(self):
        """
        Return the formatted error message for print().
        """
        return self.error_message

    def __repr__(self):
        """
        Representation for developer use (e.g. in logs, console).
        """
        return f"{self.__class__.__name__}()"
