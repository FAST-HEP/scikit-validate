import os
from importlib import import_module

import yaml
from jinja2 import Template
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from .. import __skvalidate_root__


def make_report(config):
    pass


class Report(object):
    """Compiles a report in Markdown format."""

    def __init__(self, yamlConfig):
        """Create a report from a yaml config.

        @param yamlConfig: yaml config dictionary
        """
        # 'general' is just a section from here on
        self.__general = Section(**yamlConfig, section_name='general')
        # self.__template = yamlConfig['general'].pop('template')
        # self.__properties = yamlConfig['general']
        # self.__values = {}

        # self.__sections = yamlConfig.pop('sections')

        # self.__content = ''

        # __check_template__(self.__template, 'general')
        # for name, content in self.__properties.items():
        #     value = __fill_property__(name, content)
        #     self.__values.update(value)

    @staticmethod
    def from_yaml(path):
        '''
        '''
        config = read_config(path)
        return Report(config)

    def write(self, outputFile):
        content = self.__general.content
        with open(outputFile, 'w') as f:
            f.write(content)

    def __repr__(self):
        repr = 'Output file: {}\n'
        repr += 'Template: {}\n'
        repr += 'Properties: {}\n'
        repr += 'Sections:\n {}'

        return repr.format(
            self.__output_file,
            self.__template,
            str(self.__values),
            '\n'.join(__repr_section__(k, v) for k, v in self.__sections.items()))


class Section(object):
    def __init__(self, section_name, **kwargs):
        sections = kwargs.pop('sections', {})
        self.__template = kwargs.pop('template')
        self.__name = section_name
        # TODO: not just general
        __check_template__(self.__template, 'general')
        # everything else is a property
        self.__properties = kwargs
        self.__values = {}
        self.__sections = {}
        self.__filled = False
        self.__content = ''

        for name, content in sections.items():
            self.__sections[name] = Section(**content, section_name=name)

    def __fill__(self):
        with open(self.__template) as f:
            self.__content = Template(f.read())

        for name, content in self.__properties.items():
            value = __fill_property__(name, content)
            self.__values.update(value)

        for name, section in self.__sections.items():
            self.__values[name] = section.content
        self.__content = self.__content.render(
            **self.__values
        )
        self.__filled = True

    @property
    def content(self):
        if not self.__filled:
            try:
                self.__fill__()
            except (UndefinedError, TemplateSyntaxError, TypeError) as e:
                print('Unable to render section "{}": {}'.format(self.__name, e))
                print('Section values:', self.__values)
        return self.__content


def read_config(path):
    with open(path) as f:
        config_tpl = Template(f.read())
    config = config_tpl.render(scikit_validate=__skvalidate_root__)
    config = yaml.load(config)
    return config


def __check_template__(path, section):
    if not os.path.exists(path):
        raise IOError('Could not find template "{}" for section {}'.format(path, section))


def __fill_property__(name, content):
    ''' Fills property with values. A property is a dictionary of the type
        {name: content}
        where the content can either be a value (e.g. string) or a function
        or
        {name: {function:<include for python function, param1:v1, param2:v2, ...}}

        @param name: name of the property
        @param: content: content of the property
    '''
    if isinstance(content, dict):
        func_path = content.pop('function')
        tokens = func_path.split('.')
        func_module, func_name = '.'.join(tokens[:-1]), tokens[-1]
        params = content
        m = import_module(func_module)
        func = getattr(m, func_name)
        return {name: func(**params)}
    else:
        return {name: content}


def __repr_section__(name, section):
    repr = '  name: {}\n'
    repr += '  template: {}\n'
    repr += '  properties: {}\n'
    return repr.format(
        name,
        section.pop('template'),
        str(section),
    )
