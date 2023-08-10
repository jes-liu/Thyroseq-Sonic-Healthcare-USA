# crontab

\# m h  dom mon dow   command

@monthly /opt/pydev/jesse/automation/leads_monthly_samples/venv/bin/python /opt/pydev/jesse/automation/leads_monthly_samples/scripts/main.py

@monthly /opt/pydev/jesse/automation/tps_monthly_reports/venv/bin/python /opt/pydev/jesse/automation/tps_monthly_reports/scripts/main.py

@monthly /opt/pydev/jesse/automation/qc_monthly_plots/venv/bin/python /opt/pydev/jesse/automation/qc_monthly_plots/scripts/main.py
