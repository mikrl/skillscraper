pylint ./skillscraper
ret_pylint=$?

black --check ./skillscraper
ret_black=$?

NC='\033[0m' # No Color
RED='\033[0;31m'
GREEN='\033[1;32m'

if [[ ${ret_pylint} -ne 0 ]] || [[ ${ret_black} -ne 0 ]];
then

    echo -e "${RED}Static checks failed${NC}"
else
    echo "${GREEN}Static checks passed${NC}"
fi
