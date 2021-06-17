# # import asyncio
# #
# # async def kek():
# #     while True:
# #         await asyncio.sleep(1)
# #         print('1 second')
# #
# # async def lol():
# #     while True:
# #         await asyncio.sleep(5)
# #         print('5 seconds')
# #
# # async def gather(){
# #     kek()
# # }
# #
# # asyncio.run(gather())
#
#
# import asyncio
#
#
# async def count(counter):
#     print(f"Количество записей в списке {len(counter)}")
#     while True:
#         await asyncio.sleep(1 / 1000)
#         counter.append(1)
#
#
# async def print_every_sec(counter):
#     while True:
#         await asyncio.sleep(1)
#         print(f'- 1 секунда прошла. '
#               f'Количество записей в списке: {len(counter)}')
#
#
# async def print_every_5_sec():
#     while True:
#         await asyncio.sleep(5)
#         print(f'---- 5 секунд прошло')
#
#
# async def print_every_10_sec():
#     while True:
#         await asyncio.sleep(10)
#         print(f'---------- 10 секунд прошло')
#
#
# async def main():
#     counter = list()
#     tasks = [
#         count(counter),
#         print_every_sec(counter),
#         print_every_5_sec(),
#         print_every_10_sec()
#     ]
#     await asyncio.gather(*tasks)
#
#
# asyncio.run(main())
l = [1,2,3,4,5,6,7]
print(l[2:])
