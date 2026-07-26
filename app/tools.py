from analysis import make_report
from journal import (
    build_statistics_text,
    build_last_trades_text
)


def btc_analysis_tool(user_id):

    return make_report()


def statistics_tool(user_id):

    return build_statistics_text(
        user_id
    )


def last_trades_tool(user_id):

    return build_last_trades_text(
        user_id
    )