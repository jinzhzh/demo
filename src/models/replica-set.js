/** ReplicaSet：迷你编排域模块。 */
export class ReplicaSet {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReplicaSet = (data={}) => new ReplicaSet(data);
