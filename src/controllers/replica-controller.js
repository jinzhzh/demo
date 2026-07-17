/** ReplicaController：迷你编排域模块。 */
export class ReplicaController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReplicaController = (data={}) => new ReplicaController(data);
