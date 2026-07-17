/** DnsRecord：迷你编排域模块。 */
export class DnsRecord {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createDnsRecord = (data={}) => new DnsRecord(data);
