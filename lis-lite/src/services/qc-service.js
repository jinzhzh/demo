export class 质控服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  判定({ 批次ID, 合格, 操作人ID }) {
    const 批次 = this.数据库.批次.find(x => x.id === 批次ID); if (!批次) throw new Error('质控批次不存在');
    批次.质控状态 = 合格 ? '合格' : '失控';
    const 受影响结果 = this.数据库.结果.filter(x => x.批次ID === 批次ID && x.状态 !== '已签发');
    if (!合格) 受影响结果.forEach(x => x.状态 = '已锁定');
    this.审计.记录('HOSP-A', 操作人ID, 合格 ? '质控合格' : '质控失控并锁定报告', '仪器批次', 批次ID, { 受影响结果: 受影响结果.map(x => x.id) }); return 批次;
  }
  解除锁定({ 批次ID, 操作人ID }) {
    const 批次 = this.数据库.批次.find(x => x.id === 批次ID); if (!批次 || 批次.质控状态 !== '失控') throw new Error('仅失控批次可解除锁定');
    批次.质控状态 = '已恢复'; this.数据库.结果.filter(x => x.批次ID === 批次ID && x.状态 === '已锁定').forEach(x => x.状态 = '待初审');
    this.审计.记录('HOSP-A', 操作人ID, '解除质控锁定', '仪器批次', 批次ID); return 批次;
  }
}
