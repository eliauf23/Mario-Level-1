using unittest for test framework

using pytest for tags - not implemented yet
```python

import pytest

@pytest.mark.unittest
def test_sample_case():
    assert 1 == 1


```

We're using:
@pytest.mark.unittest (unit test)
@pytest.mark.integration (integration test)
@pytest.mark.xfail (expected faliure)

maybe we also want to tag mocks etc. to keep stuff organized