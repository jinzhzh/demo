/** Pod：迷你编排域模块。 */
export class Pod {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createPod = (data={}) => new Pod(data);
