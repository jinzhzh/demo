/** Admission：迷你编排域模块。 */
export class Admission {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createAdmission = (data={}) => new Admission(data);
