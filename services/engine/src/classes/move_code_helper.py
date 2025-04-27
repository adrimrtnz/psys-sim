from src.enums.constants import MoveCodes

class MoveCodeHelper:

    @staticmethod
    def get_move_code(code: str):
        """Get the value of a move description"""
        move_code = MoveCodes.__members__.get(code, None)
        if move_code:
            return move_code.value
        raise ValueError(f'The code {code} is not a valid MoveCode.')
    
    @staticmethod
    def has_son_destination(value: int):
        return value == MoveCodes.IN.value
    
    @staticmethod
    def has_brother_destination(value: int):
        valid_destination = [
            MoveCodes.MEM.value,
            MoveCodes.MEM_WC.value,
            MoveCodes.MEM_TRANS.value,
            MoveCodes.GROUP_TRANS.value,
            MoveCodes.MEM_W_OB.value,
            MoveCodes.DMEM.value]
        return value in valid_destination