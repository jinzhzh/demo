/** ScoreChain：迷你编排域模块。 */
export class ScoreChain {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createScoreChain = (data={}) => new ScoreChain(data);
