/** Toleration：迷你编排域模块。 */
export class Toleration {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createToleration = (data={}) => new Toleration(data);
