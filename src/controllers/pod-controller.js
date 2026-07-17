/** PodController：迷你编排域模块。 */
export class PodController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createPodController = (data={}) => new PodController(data);
