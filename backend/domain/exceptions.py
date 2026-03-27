"""Exceções de domínio do sistema Viaje Bem."""


class InvalidCredentialsError(Exception):
    """Levantada quando email/senha do admin são inválidos ou role não é ADMIN."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message)


class AdminTokenInvalidError(Exception):
    """Levantada quando o JWT do admin é inválido, expirado ou com role incorreta."""

    def __init__(self, message: str = "Token de autenticação inválido"):
        super().__init__(message)


class OverbookingError(Exception):
    """Levantada quando a reserva excede as vagas disponíveis na viagem."""

    def __init__(self, available: int):
        super().__init__(
            f"Vagas insuficientes. Disponível: {available}"
        )
        self.available = available


class TripNotFoundError(Exception):
    """Levantada quando a viagem especificada não existe."""

    def __init__(self, trip_id: str):
        super().__init__(f"Viagem não encontrada: {trip_id}")


class PassengerFormLockedError(Exception):
    """Levantada quando o líder tenta cadastrar acompanhantes com reserva em status CREATED."""

    def __init__(self):
        super().__init__(
            "Formulário de acompanhantes bloqueado. Aguarde a confirmação do sinal pela agência."
        )
