{
    "name": "EcoSphere ESG",
    "version": "18.0.1.0.0",
    "category": "Human Resources",
    "summary": "ESG (Environmental, Social, Governance) Management Platform with Gamification",
    "description": """
EcoSphere ESG
=============
Track carbon emissions, run CSR activities and gamified challenges, manage
governance policies, audits and compliance issues, and score departments
across Environmental, Social and Governance dimensions. Includes a
dashboard, leaderboard and a badge/reward gamification engine.
""",
    "author": "kaushik jasoliya",
    "license": "LGPL-3",
    "depends": ["base", "mail", "web"],
    "data": [
        "security/esg_security.xml",
        "security/ir.model.access.csv",
        "security/esg_security_rules.xml",
        "data/esg_sequence_data.xml",
        "data/esg_mail_template_data.xml",
        "data/esg_cron_data.xml",
        "data/esg_demo_data_full.xml",
        "views/esg_department_views.xml",
        "views/esg_employee_views.xml",
        "views/esg_category_views.xml",
        "views/esg_emission_factor_views.xml",
        "views/esg_product_profile_views.xml",
        "views/esg_environmental_goal_views.xml",
        "views/esg_policy_views.xml",
        "views/esg_badge_views.xml",
        "views/esg_reward_views.xml",
        "views/esg_carbon_transaction_views.xml",
        "views/esg_csr_activity_views.xml",
        "views/esg_employee_participation_views.xml",
        "views/esg_challenge_views.xml",
        "views/esg_challenge_participation_views.xml",
        "views/esg_policy_acknowledgement_views.xml",
        "views/esg_audit_views.xml",
        "views/esg_compliance_issue_views.xml",
        "views/esg_department_score_views.xml",
        "views/esg_leaderboard_views.xml",
        "views/res_config_settings_views.xml",
        "views/esg_dashboard_views.xml",
        "views/dashboard_templates.xml",
        "views/esg_menus.xml",
        "report/esg_summary_report.xml",
        "report/esg_summary_report_templates.xml",
    ],
    "demo": [
        "data/esg_demo_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ecosphere_esg/static/src/js/**/*.js",
            "ecosphere_esg/static/src/xml/**/*.xml",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}