/** Affinity：迷你编排域模块。 */
export class Affinity {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createAffinity = (data={}) => new Affinity(data);
