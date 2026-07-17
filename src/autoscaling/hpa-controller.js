/** HpaController：迷你编排域模块。 */
export class HpaController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createHpaController = (data={}) => new HpaController(data);
