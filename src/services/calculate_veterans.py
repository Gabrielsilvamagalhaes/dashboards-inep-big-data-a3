def calculateVeterans(total_matriculados: int, total_ingressantes: int) -> int:
    return max(total_matriculados - total_ingressantes, 0)
