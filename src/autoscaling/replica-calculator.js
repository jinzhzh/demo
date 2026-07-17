/** ReplicaCalculator：迷你编排域模块。 */
export class ReplicaCalculator {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReplicaCalculator = (data={}) => new ReplicaCalculator(data);
