# Copyright (c) 2023, INRIA
# Copyright (c) 2023, University of Lille
# All rights reserved.
import copy

import pytest

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from powerapi.cli.binding_manager import PreProcessorBindingManager
from powerapi.dispatcher import DispatcherActor
from powerapi.exception import PowerAPIException, UnsupportedActorTypeException, BadInputData, UnexistingActorException, \
    TargetActorAlreadyUsed
from powerapi.processor.processor_actor import ProcessorActor


def check_default_pre_processor_binding_manager_default_actors_content(processor_manager: PreProcessorBindingManager):
    """
    Check the default size for actors dictionary of the manager
    :param PreProcessorBindingManager processor_manager: Binding manager to check the size
    """
    assert len(processor_manager.actors) == 0
    assert len(processor_manager.processors) == 0


def test_create_pre_processor_binding_manager_with_actors(pre_processor_pullers_and_processors_dictionaries):
    """
    Test that a PreProcessorBindingManager is correctly created when an actor and a processor dictionary are provided
    """
    expected_actors_dictionary = copy.copy(pre_processor_pullers_and_processors_dictionaries[0])
    expected_processors_dictionary = copy.copy(pre_processor_pullers_and_processors_dictionaries[1])

    binding_manager = PreProcessorBindingManager(actors=pre_processor_pullers_and_processors_dictionaries[0],
                                                 processors=pre_processor_pullers_and_processors_dictionaries[1])

    assert binding_manager.actors == expected_actors_dictionary
    assert binding_manager.processors == expected_processors_dictionary


def test_create_processor_binding_manager_without_actors():
    """
    Test that a ProcessorBindingManager is correctly created without a dictionary
    """
    binding_manager = PreProcessorBindingManager(actors=None, processors=None)

    check_default_pre_processor_binding_manager_default_actors_content(processor_manager=binding_manager)


def test_process_bindings_for_pre_processor(pre_processor_complete_configuration,
                                            pre_processor_pullers_and_processors_dictionaries):
    """
    Test that the bindings between a puller and a processor are correctly created
    """
    pullers = pre_processor_pullers_and_processors_dictionaries[0]
    processors = pre_processor_pullers_and_processors_dictionaries[1]

    binding_manager = PreProcessorBindingManager(actors=pullers,
                                                 processors=processors)

    assert len(pullers['one_puller'].state.report_filter.filters) == 1
    assert isinstance(pullers['one_puller'].state.report_filter.filters[0][1], DispatcherActor)

    binding_manager.process_bindings()

    assert len(pullers['one_puller'].state.report_filter.filters) == 1
    assert isinstance(pullers['one_puller'].state.report_filter.filters[0][1], ProcessorActor)
    assert pullers['one_puller'].state.report_filter.filters[0][1] == processors['my_processor']


def test_process_bindings_for_pre_processor_raise_exception_with_wrong_binding_types(
        pre_processor_binding_manager_with_wrong_binding_types):
    """
    Test that an exception is raised with a wrong type for the from actor in a binding
    """

    with pytest.raises(UnsupportedActorTypeException):
        pre_processor_binding_manager_with_wrong_binding_types.process_bindings()


def test_process_bindings_for_pre_processor_raise_exception_with_no_existing_puller(
        pre_processor_binding_manager_with_unexisting_puller):
    """
    Test that an exception is raised with a puller that doesn't exist
    """

    with pytest.raises(UnexistingActorException):
        pre_processor_binding_manager_with_unexisting_puller.process_bindings()


def test_process_bindings_for_pre_processor_raise_exception_with_reused_puller_in_bindings(
        pre_processor_binding_manager_with_reused_puller_in_bindings):
    """
    Test that an exception is raised when the same puller is used by several processors
    """

    with pytest.raises(TargetActorAlreadyUsed):
        pre_processor_binding_manager_with_reused_puller_in_bindings.process_bindings()


def test_check_processors_targets_are_unique_raise_exception_with_reused_puller_in_bindings(
        pre_processor_binding_manager_with_reused_puller_in_bindings):
    """
    Test that an exception is raised when the same puller is used by several processors
    """
    with pytest.raises(TargetActorAlreadyUsed):
        pre_processor_binding_manager_with_reused_puller_in_bindings.check_processors_targets_are_unique()


def test_check_processors_targets_are_unique_pass_without_reused_puller_in_bindings(
        pre_processor_binding_manager):
    """
    Test that a correct without repeated target passes the validation
    """
    try:
        pre_processor_binding_manager.check_processors_targets_are_unique()
        assert True
    except TargetActorAlreadyUsed:
        assert False


def test_check_processor_targets_raise_exception_with_no_existing_puller(
        pre_processor_binding_manager_with_unexisting_puller):
    """
    Test that an exception is raised with a puller that doesn't exist
    """
    pre_processor_binding_manager = pre_processor_binding_manager_with_unexisting_puller
    with pytest.raises(UnexistingActorException):
        for _, processor in pre_processor_binding_manager.processors.items():
            pre_processor_binding_manager.check_processor_targets(processor=processor)


def test_check_processor_targets_raise_exception_with_raise_exception_with_wrong_binding_types(
        pre_processor_binding_manager_with_wrong_binding_types):
    """
    Test that an exception is raised with a puller that doesn't exist
    """
    pre_processor_binding_manager = pre_processor_binding_manager_with_wrong_binding_types
    with pytest.raises(UnsupportedActorTypeException):
        for _, processor in pre_processor_binding_manager.processors.items():
            pre_processor_binding_manager.check_processor_targets(processor=processor)


def test_check_processor_targets_pass_with_correct_targets(pre_processor_binding_manager):
    """
    Test that validation of a configuration with existing targets of the correct type
    """
    try:
        for _, processor in pre_processor_binding_manager.processors.items():
            pre_processor_binding_manager.check_processor_targets(processor=processor)

        assert True
    except UnsupportedActorTypeException:
        assert False
    except UnexistingActorException:
        assert False
