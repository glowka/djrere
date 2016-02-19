import React, { Component } from 'react';
import { Link } from 'react-router';

import './Header.less';


export default class Header extends Component {
  render() {
    return (
      <header>

        Ordinary header
        <Link to="../">Blog</Link>
        <Link to="./child/">Child</Link>
      </header>
    );
  }
}
