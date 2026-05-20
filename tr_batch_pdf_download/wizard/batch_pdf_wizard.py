import ast
import io
import zipfile
import base64

from odoo import _, api, fields, models
from odoo.exceptions import UserError


REPORT_MAP = {
    'account.move':    ('account.report_invoice',            '{name}.pdf'),
    'sale.order':      ('sale.action_report_saleorder',      '{name}.pdf'),
    'purchase.order':  ('purchase.report_purchase_order',    '{name}.pdf'),
    'stock.picking':   ('stock.action_report_picking',       '{name}.pdf'),
}


class BatchPdfWizard(models.TransientModel):
    _name = 'tr.batch.pdf.wizard'
    _description = 'Batch PDF Download'

    model = fields.Char(readonly=True)
    res_ids = fields.Char(readonly=True)
    record_count = fields.Integer(compute='_compute_record_count')

    @api.depends('res_ids')
    def _compute_record_count(self):
        for rec in self:
            try:
                ids = ast.literal_eval(rec.res_ids or '[]')
                rec.record_count = len(ids)
            except Exception:
                rec.record_count = 0

    def _get_ids(self):
        try:
            return ast.literal_eval(self.res_ids or '[]')
        except Exception:
            return []

    def action_download(self):
        self.ensure_one()
        model = self.model
        ids = self._get_ids()

        if not ids:
            raise UserError(_('No records selected.'))

        if model not in REPORT_MAP:
            raise UserError(_('Batch PDF download is not supported for %s.') % model)

        report_name, filename_tpl = REPORT_MAP[model]
        records = self.env[model].browse(ids)

        zip_buffer = io.BytesIO()
        generated = 0

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for record in records:
                try:
                    pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                        report_name, [record.id]
                    )
                    rec_name = (record.name or str(record.id)).replace('/', '_')
                    filename = filename_tpl.format(name=rec_name)
                    zf.writestr(filename, pdf_content)
                    generated += 1
                except Exception as e:
                    # Skip failed records, continue with rest
                    continue

        if generated == 0:
            raise UserError(_('Could not generate any PDFs. Please check report configuration.'))

        zip_buffer.seek(0)
        zip_data = base64.b64encode(zip_buffer.read())

        # Save as attachment and return download
        attachment = self.env['ir.attachment'].create({
            'name': f'batch_download_{model.replace(".", "_")}.zip',
            'type': 'binary',
            'datas': zip_data,
            'mimetype': 'application/zip',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
