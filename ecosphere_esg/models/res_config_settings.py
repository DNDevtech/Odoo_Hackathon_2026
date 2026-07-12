# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    require_proof = fields.Boolean(
        string="Require Proof for CSR/Challenge Approval",
        config_parameter="ecosphere_esg.require_proof",
    )
    auto_emission_calc = fields.Boolean(
        string="Auto Emission Calculation",
        config_parameter="ecosphere_esg.auto_emission_calc",
    )
    badge_auto_award = fields.Boolean(
        string="Badge Auto-Award",
        default=True,
        config_parameter="ecosphere_esg.badge_auto_award",
    )
    weight_environmental = fields.Float(
        string="Environmental Weight (%)",
        default=40.0,
        config_parameter="ecosphere_esg.weight_environmental",
    )
    weight_social = fields.Float(
        string="Social Weight (%)",
        default=30.0,
        config_parameter="ecosphere_esg.weight_social",
    )
    weight_governance = fields.Float(
        string="Governance Weight (%)",
        default=30.0,
        config_parameter="ecosphere_esg.weight_governance",
    )
    notify_compliance_issue = fields.Boolean(
        string="Notify on New Compliance Issue",
        default=True,
        config_parameter="ecosphere_esg.notify_compliance_issue",
    )
    notify_challenge_decision = fields.Boolean(
        string="Notify on Challenge Approval/Rejection",
        default=True,
        config_parameter="ecosphere_esg.notify_challenge_decision",
    )
    notify_csr_decision = fields.Boolean(
        string="Notify on CSR Approval/Rejection",
        default=True,
        config_parameter="ecosphere_esg.notify_csr_decision",
    )
    notify_policy_reminder = fields.Boolean(
        string="Notify Policy Acknowledgement Reminders",
        default=True,
        config_parameter="ecosphere_esg.notify_policy_reminder",
    )
    notify_badge_unlock = fields.Boolean(
        string="Notify on Badge Unlock",
        default=True,
        config_parameter="ecosphere_esg.notify_badge_unlock",
    )
