/** LeastAllocatedScore：迷你编排域模块。 */
export class LeastAllocatedScore {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createLeastAllocatedScore = (data={}) => new LeastAllocatedScore(data);
