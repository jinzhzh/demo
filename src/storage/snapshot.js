/** Snapshot：迷你编排域模块。 */
export class Snapshot {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createSnapshot = (data={}) => new Snapshot(data);
