/** Reason：迷你编排域模块。 */
export class Reason {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReason = (data={}) => new Reason(data);
