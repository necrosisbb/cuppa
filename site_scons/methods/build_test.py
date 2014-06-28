
#          Copyright Jamie Allsop 2011-2014
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

#-------------------------------------------------------------------------------
#   BuildTestMethod
#-------------------------------------------------------------------------------


class BuildTestMethod:

    def __init__( self, toolchain, default_test_runner=None ):
        self._toolchain = toolchain
        self._default_test_runner = default_test_runner


    def __call__( self, env, target, source, final_dir=None, data=None, append_variant=None, test_runner=None, expected='success' ):
        program = env.Build( target, source, final_dir=final_dir, append_variant=append_variant )
        if env['variant_actions'].has_key('test'):
            if not test_runner:
                test_runner = self._default_test_runner
            env.Test( program, final_dir=final_dir, data=data, test_runner=test_runner, expected=expected )
            if env['variant_actions'].has_key('coverage'):
                env.Coverage( program, final_dir=final_dir )
        return program


    @classmethod
    def add_to_env( cls, args ):
        args['env'].AddMethod( cls( args['env']['toolchain'], args['env']['default_test_runner'] ), "BuildTest" )
        for test_runner in args['env']['toolchain'].test_runners():
            args['env'].AddMethod( cls( args['env']['toolchain'], test_runner ), "Build{}Test".format( test_runner.title() ) )
