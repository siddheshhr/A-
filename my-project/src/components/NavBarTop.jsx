import React, { useState, useEffect } from 'react';
import { Navbar, TextInput, Button } from 'flowbite-react';
import { AiOutlineSearch } from 'react-icons/ai';

const NavBarTop = () => {
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const searchTermFromUrl = urlParams.get('searchTerm');
    if (searchTermFromUrl) {
      setSearchTerm(searchTermFromUrl);
    }
  }, [window.location.search]);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Search Term:', searchTerm);
  };

  return (
    <div>
      <Navbar className="border-b-2">
        <span className=" self-center whitespace-nowrap text-sm sm:text-xl font-semibold px-2 py-1 bg-gradient-to-r from-cyan-800 via-cyan-700 to-blue-500 rounded-lg text-white">
          MahaNavi
        </span>

        <form onSubmit={handleSubmit} className="flex items-center">
          <TextInput
            type="text"
            placeholder="Search..."
            icon={AiOutlineSearch}
            className="lg:inline mr-2 w-82"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <Button type="submit" gradientMonochrome="info" className='px-1 mr-2 w-32' >
            Source
          </Button>
          <TextInput
            type="text"
            placeholder="Search..."
            icon={AiOutlineSearch}
            className="lg:inline mr-2 w-82 "
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <Button type="submit" gradientMonochrome="purple" className='w-32 px-1 mr-2'>
            Destination
          </Button>
        </form>

        <Button className="w-12 h-10 lg:hidden bg-gray-300 text-black-700 font-semibold" pill>
          <AiOutlineSearch />
        </Button>

        <Navbar.Collapse>
          <Navbar.Link href="#">Home</Navbar.Link>
          <Navbar.Link href="#">About</Navbar.Link>
          <Navbar.Link href="#">Explore</Navbar.Link>
        </Navbar.Collapse>
      </Navbar>
    </div>
  );
};

export default NavBarTop;
