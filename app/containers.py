from dependency_injector import containers, providers
from api.wallets.use_cases import ListWallets
from config import Settings
from db.database import get_session
from db.database2 import Database2
from repositories.wallet_repository import WalletRepository
from repositories.wallet_repository2 import WalletRepository2

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "routes",
            "api.wallets.views",
        ]
    )

    # settingsProvider = providers.ThreadSafeSingleton(Settings)
    
    # print("eeeeeeeeeeeeeeeeeeeeeeeeeee")
    env = Settings()
    print(env.status)
    if env.status == "testing":
        # テスト環境のDIを設定
        print("a")
    else:
        print("b")
        db = providers.Singleton(Database2, db_url=env.db_url)

        walletRepositoryProvider = providers.Factory(
            WalletRepository2,
            session=db.provided.session,
        )

        listWalletProvider = providers.Factory(
            ListWallets,
            # session=get_session,
            repo=walletRepositoryProvider,
        )

    # config = providers.Configuration(yaml_files=["config.yml"])

    # test = providers.Factory(
    #     Test,
    #     config=settings,
    # )