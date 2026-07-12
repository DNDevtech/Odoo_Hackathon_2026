from odoo import models, fields, api
from datetime import datetime, timedelta


class EcoSphereDashboard(models.TransientModel):
    _name = "ecosphere_esg.dashboard"
    _description = "EcoSphere Dashboard"

    name = fields.Char(default="EcoSphere Dashboard")
    html = fields.Html(compute="_compute_html", sanitize=False)

    def _compute_html(self):
        for rec in self:
            rec.html = self.env['ir.qweb']._render('ecosphere_esg.dashboard_content', self._values())

    def _values(self):
        env = self.env
        scores = env['esg.department.score'].search([])
        n = max(len(scores), 1)
        kpi = {
            'environmental': round(sum(s.environmental_score for s in scores) / n, 1),
            'social': round(sum(s.social_score for s in scores) / n, 1),
            'governance': round(sum(s.governance_score for s in scores) / n, 1),
            'overall': round(sum(s.total_score for s in scores) / n, 1),
        }
        carbon = env['esg.carbon.transaction'].search([])
        total_emission = sum(c.emission_kgco2e for c in carbon)
        _rank = sorted(
            [{'name': s.department_id.name, 'total': s.total_score} for s in scores],
            key=lambda r: r['total'], reverse=True)
        max_rank = max((r['total'] for r in _rank), default=100) or 100
        ranking = [dict(r, style="width:%d%%" % round(r['total'] / max_rank * 100)) for r in _rank]
        today = datetime.today()
        months = [(today - timedelta(days=30 * i)).replace(day=1) for i in range(11, -1, -1)]
        trend = []
        for m in months:
            nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
            val = sum(c.emission_kgco2e for c in carbon
                      if c.date and m <= datetime(c.date.year, c.date.month, 1) < nxt)
            trend.append({'label': m.strftime('%b'), 'value': round(val, 1)})
        max_trend = max((t['value'] for t in trend), default=1) or 1
        for t in trend:
            pct = round(t['value'] / max_trend * 100) if max_trend else 0
            t['style'] = "height:%d%%" % pct

        def act(xmlid):
            return '/web#action=%s' % env.ref(xmlid).id

        return {
            'kpi': kpi,
            'total_emission': round(total_emission, 1),
            'compliance_open': env['esg.compliance.issue'].search_count([('state', '=', 'open')]),
            'active_challenges': env['esg.challenge'].search_count([('state', '=', 'active')]),
            'policies': env['esg.policy'].search_count([]),
            'audits': env['esg.audit'].search_count([]),
            'ranking': ranking,
            'max_rank': max_rank,
            'trend': trend,
            'max_trend': max_trend,
            'recent_carbon': carbon.sorted(key=lambda r: r.date or datetime.min, reverse=True)[:5],
            'recent_compliance': env['esg.compliance.issue'].search([], order='create_date desc', limit=5),
            'recent_challenges': env['esg.challenge'].search([], order='create_date desc', limit=5),
            'links': {
                'carbon': act('ecosphere_esg.action_esg_carbon_transaction'),
                'challenge': act('ecosphere_esg.action_esg_challenge'),
                'reports': act('ecosphere_esg.action_esg_department_score'),
                'settings': act('ecosphere_esg.action_esg_settings'),
                'csr': act('ecosphere_esg.action_esg_csr_activity'),
                'policy': act('ecosphere_esg.action_esg_policy'),
                'audit': act('ecosphere_esg.action_esg_audit'),
                'leaderboard': act('ecosphere_esg.action_esg_leaderboard'),
            },
        }
