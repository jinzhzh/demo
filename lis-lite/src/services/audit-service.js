export class 审计服务 {
  constructor(数据库) { this.数据库 = 数据库; }
  记录(机构ID, 用户ID, 动作, 对象类型, 对象ID, 详情 = {}) {
    const 事件 = { id: `AUD-${this.数据库.审计.length + 1}`, 机构ID, 用户ID, 动作, 对象类型, 对象ID, 详情, 时间: new Date().toISOString() };
    this.数据库.审计.push(事件); return 事件;
  }
}
