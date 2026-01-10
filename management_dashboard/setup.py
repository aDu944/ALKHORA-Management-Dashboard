from setuptools import setup, find_packages


setup(
    name="management_dashboard",
    version="0.0.1",
    description="ERPNext/Frappe app: annual management dashboard",
    author="ALKHORA",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

