# from fastapi import Request
# from fastapi.responses import JSONResponse
#
# class DataNotFoundError(Exception):
#     pass
#
#
# @app.exception_handler(DataNotFoundError)
# async def user_not_found_handler(exc: DataNotFoundError):
#     return JSONResponse(
#         status_code=404,
#         content={
#             "code": "Data_NOT_FOUND",
#             "message": "Data not found",
#             "details": str(exc)
#         }
#     )