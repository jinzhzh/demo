/** Status：迷你编排域模块。 */
export class Status {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createStatus = (data={}) => new Status(data);
