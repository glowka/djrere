import TestUtils from 'react/lib/ReactTestUtils';
import expect from 'expect';
import router from '../router';


describe('root', () => {
  it('renders without problems', () => {
    const root = TestUtils.renderIntoDocument(router);
    expect(root).toExist();
  });
});





