import os, filecmp, docker, subprocess

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def mycmp(file1, file2):
    with open(file1, "r") as file:
        a = file.read()
    with open(file2, "r") as file:
        b = file.read()
    return a == b

def evaluateDockerSubprocess(code, inFile, outFile):
    inFile = os.path.join('input_files', inFile)
    outFile = os.path.join('output_files', outFile)
    with open('solution.cpp', 'w') as file:
        file.write(code)
    try:
        container = client.containers.get('oj')
        if container.status != 'running':
            container.start()
    except docker.errors.NotFound:
        container = client.containers.run('gcc', command='sleep infinity', name='oj', detach=True)
    subprocess.run(['docker', 'cp', 'solution.cpp', container.id+":/a.cpp"])
    subprocess.run(['docker', 'cp', inFile, container.id+":/input.txt"])
    print(subprocess.run(['docker', 'exec', container.id, 'bash', '-c', "./a.out<input.txt>output.txt"]).returncode)
    if subprocess.run(['docker', 'exec', container.id, 'bash', '-c', "g++ a.cpp"]).returncode != 0:
        verdict = "Compilation Error"
    elif subprocess.run(['docker', 'exec', container.id, 'bash', '-c', "./a.out<input.txt>output.txt"]).returncode != 0:
        verdict = "Runtime Error"
    else:
        subprocess.run(['docker', 'cp', container.id+":/output.txt", 'out.txt'])
        with open('out.txt', 'r') as file:
            text = file.read()
        with open('out.txt', 'w') as file:
            file.write(text)
        if filecmp.cmp('out.txt', outFile, shallow=False):
            verdict = "Accepted"
        else:
            verdict = "Wrong Answer"
    if os.path.exists('out.txt'):
        os.remove('out.txt')
    return verdict

def evaluateDocker(code, inFile, outFile):
    inFile = os.path.join('input_files', inFile)
    outFile = os.path.join('output_files', outFile)
    with open('solution.cpp', 'w') as file:
        file.write(code)
    try:
        container = client.containers.get('oj')
        if container.status != 'running':
            container.start()
    except docker.errors.NotFound:
        container = client.containers.run('gcc', command='sleep infinity', name='oj', detach=True)
    print(os.system(f'docker cp solution.cpp {container.id}:/a.cpp'))
    if os.system(f'docker exec {container.id} g++ a.cpp') != 0:
        verdict = 'Compilation Error'
    elif os.system(f'docker exec -i {container.id} ./a.out < {inFile} > outdocker.txt') != 0:
        verdict = 'Runtime Error'
        print('runtime error')
    else:
        if mycmp('outdocker.txt', outFile):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
    container.stop()
    return verdict

def evaluate(code, inFile, outFile):
    inFile = os.path.join('input_files', inFile)
    outFile = os.path.join('output_files', outFile)
    with open('solution.cpp', 'w') as file:
        file.write(code)
    if os.system('g++ solution.cpp -o sol.exe') != 0:
        return 'Compilation Error'
    elif os.system(f'sol < {inFile} > out.txt') != 0:
        return 'Runtime Error'
    elif filecmp.cmp('out.txt', outFile, shallow=False):
        return 'Accepted'
    else:
        return 'Wrong Answer'