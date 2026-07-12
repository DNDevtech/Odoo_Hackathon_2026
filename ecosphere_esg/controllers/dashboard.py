from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class EcoSphereDashboard(http.Controller):

    @http.route('/eco/dashboard', type='http', auth='user', website=False)
    def dashboard(self, **kw):
        env = request.env
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
        compliance_open = env['esg.compliance.issue'].search_count([('state', '=', 'open')])
        active_challenges = env['esg.challenge'].search_count([('state', '=', 'active')])
        policies = env['esg.policy'].search_count([])
        audits = env['esg.audit'].search_count([])

        # Department ESG ranking
        ranking = sorted(
            [{'name': s.department_id.name, 'total': s.total_score,
              'env': s.environmental_score, 'soc': s.social_score, 'gov': s.governance_score}
             for s in scores],
            key=lambda r: r['total'], reverse=True)

        # Emissions trend (last 12 months)
        today = datetime.today()
        months = []
        for i in range(11, -1, -1):
            d = today - timedelta(days=30 * i)
            months.append(d.replace(day=1))
        trend = []
        for m in months:
            nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
            val = sum(c.emission_kgco2e for c in carbon
                      if c.date and m <= datetime(c.date.year, c.date.month, 1) < nxt)
            trend.append({'label': m.strftime('%b'), 'value': round(val, 1)})
        max_trend = max((t['value'] for t in trend), default=1) or 1

        # Recent activity
        recent_carbon = carbon.sorted(key=lambda r: r.date or datetime.min, reverse=True)[:5]
        recent_compliance = env['esg.compliance.issue'].search([], order='create_date desc', limit=5)
        recent_challenges = env['esg.challenge'].search([], order='create_date desc', limit=5)

        # Action links
        def act(xmlid):
            return '/web#action=%s' % env.ref(xmlid).id

        values = {
            'kpi': kpi,
            'total_emission': round(total_emission, 1),
            'compliance_open': compliance_open,
            'active_challenges': active_challenges,
            'policies': policies,
            'audits': audits,
            'ranking': ranking,
            'max_rank': max((r['total'] for r in ranking), default=100) or 100,
            'trend': trend,
            'max_trend': max_trend,
            'recent_carbon': recent_carbon,
            'recent_compliance': recent_compliance,
            'recent_challenges': recent_challenges,
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
        return request.render('ecosphere_esg.dashboard_template', values)
