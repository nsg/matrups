from matrups.transport import Transport
from matrups.matrix import Matrix, MatrixLoginCredentials
from matrups.hangouts import Hangouts, HangoutsLoginCredentials
from matrups.config import Config

def main():
    transport = Transport()
    config = Config("config.yml")

    Matrix(MatrixLoginCredentials(config.matrix("host"),
                                  config.matrix("token"),
                                  config.matrix("userid")),
           config.matrix("rooms"),
           config.bridge("matrix_to"),
           transport
        )

    h = Hangouts(HangoutsLoginCredentials(config.hangouts("email"),
                                          config.hangouts("password"),
                                          config.hangouts("token_file")),
                 config.bridge("hangouts_to"),
                 transport)

    h.loop()

if __name__ == '__main__':
    main()

