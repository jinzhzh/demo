/** ClusterConfig：迷你编排域模块。 */
export class ClusterConfig {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createClusterConfig = (data={}) => new ClusterConfig(data);
