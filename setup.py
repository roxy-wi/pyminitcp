from setuptools import setup, find_packages

setup(
    name="pyminitcp",
    version="2.0.0",
    description="A tiny, dependency-free Python library for TCP and UDP connectivity checks with IPv4/IPv6 and DNS support.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Pavel Loginov",
    author_email="aidaho@roxy-wi.org",
    url="https://github.com/roxy-wi/pyminitcp",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking",
    ],
    keywords="tcp udp network check ipv6 ipv4 monitoring",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pyminitcp=pyminitcp.cli:main"
        ]
    },
)
