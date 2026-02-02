from rocketry import Rocketry
from rocketry.conds import every

from main import main  # this calls your email automation

app = Rocketry()


@app.task(every("30 seconds"))
def run_email_automation():
    print("🚀 Rocketry triggered email automation")
    main()
    print("✅ Email automation cycle finished")


if __name__ == "__main__":
    print("🕒 Rocketry scheduler started (every 5 minutes)")
    app.run()