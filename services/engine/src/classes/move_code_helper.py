from src.enums.constants import MoveCode

class MoveCodeHelper:

    @staticmethod
    def get_move_code(code: str):
        """Get the value of a move description"""
        move_code = MoveCode.__members__.get(code, None)
        if move_code:
            return move_code.value
        raise ValueError(f'The code {code} is not a valid MoveCode.')
    
    @staticmethod
    def has_son_destination(value: int):
        return value == MoveCode.IN.value
    
    @staticmethod
    def has_brother_destination(value: int):
        valid_destination = [
            MoveCode.MEM.value,
            MoveCode.MEMWC.value,
            MoveCode.MEMTRANS.value,
            MoveCode.GROUP_TRANS.value,
            MoveCode.MEMwOB.value,
            MoveCode.DMEM.value]
        return value in valid_destination