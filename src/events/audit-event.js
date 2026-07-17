/** AuditEvent：迷你编排域模块。 */
export class AuditEvent {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createAuditEvent = (data={}) => new AuditEvent(data);
