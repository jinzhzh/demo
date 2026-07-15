import { 解析HL7, 应答 } from '../hl7/parser.js';
import { 标本状态 } from '../domain/enums.js';

export class 仪器服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  创建批次({ 仪器ID, 批次号 }) { const 批次 = { id: `BATCH-${批次号}`, 仪器ID, 批次号, 质控状态: '待质控' }; this.数据库.批次.push(批次); return 批次; }
  接收HL7({ 机构ID, 仪器ID, 批次ID, 文本, 操作人ID }) {
    const r = 解析HL7(文本), 标本 = this.数据库.标本.find(x => x.id === r.标本ID && x.机构ID === 机构ID);
    if (!标本 || !标本.项目ID列表.includes(r.项目ID)) throw new Error('无法根据报文匹配标本或检验项目');
    const 项目 = this.数据库.项目.find(x => x.id === r.项目ID), 危急 = r.结果值 <= 项目.危急低值 || r.结果值 >= 项目.危急高值;
    const 结果 = { id: `RES-${this.数据库.结果.length + 1}`, 标本ID: 标本.id, 项目ID: r.项目ID, 批次ID, 值: r.结果值, 单位: r.单位, 危急, 状态: '待初审', 版本: 1, 签署: [] };
    this.数据库.结果.push(结果); 标本.结果.push(结果.id); 标本.状态 = 标本状态.待审核;
    this.数据库.仪器报文.push({ ...r, 仪器ID, 状态: '已解析' });
    if (危急) this.数据库.危急值.push({ id: `CA-${this.数据库.危急值.length + 1}`, 结果ID: 结果.id, 状态: '待双签', 通知状态: '待通知', 签署: [] });
    this.审计.记录(机构ID, 操作人ID, '接收仪器结果', '结果', 结果.id, { 危急, 批次ID }); return { 结果, 应答: 应答(r.消息ID) };
  }
}
