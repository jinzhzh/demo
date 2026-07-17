/** RestartPolicy：迷你编排域模块。 */
export class RestartPolicy {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRestartPolicy = (data={}) => new RestartPolicy(data);
